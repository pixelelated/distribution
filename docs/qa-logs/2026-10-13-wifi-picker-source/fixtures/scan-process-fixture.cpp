// UNRUN. Compile/run only in the coordinator's allocated disposable Linux job.
// Include the actual proposed helper via -I <ES>/es-app/src/guis. No ES renderer
// or network backend is needed. Emits child/group identities, never uses a
// broad process-name kill. An outer runner must enforce job-wide teardown.
#include "WifiScanProcess.h"
#include <cassert>
#include <iostream>
#include <sys/prctl.h>
#include <utility>
#ifdef NDEBUG
#error Compile this fixture with assertions enabled.
#endif

int main()
{
	using namespace std::chrono;
	// This test becomes the reaper for deliberately orphaned grandchildren;
	// the production helper relies on the VM's normal init/reaper instead.
	assert(prctl(PR_SET_CHILD_SUBREAPER, 1) == 0);
	const auto run = [](const std::string& script, milliseconds timeout = seconds(1))
	{
		return WifiScanProcess::read({"/bin/sh", "-c", script}, timeout);
	};
	const auto names = run("printf 'Leading and trailing  \\nCafe: Guest\\nlast-without-newline'");
	assert(names.code == 0 && names.lines.size() == 3);
	assert(names.lines[0] == "Leading and trailing  ");
	assert(names.lines[2] == "last-without-newline");
	assert(run("exit 0").code == 0);
	const auto failure = run("printf 'discard-this\\n'; exit 2");
	assert(failure.code == 2 && failure.lines.empty());
	assert(run("kill -TERM $$").code == -1);
	assert(WifiScanProcess::read({"/definitely-absent-wifi-577-command"}, seconds(1)).code == -1);
	assert(run("while :; do printf 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\\n'; done").code == -1);

	// Cover driver alive, driver exited with a pipe-holding descendant, and
	// driver exited with a descendant that closed stdout. All must be cleaned.
	const std::vector<std::pair<std::string, int>> cases{
		{"trap '' TERM; echo driver=$$ >&2; sh -c 'sleep 30 & echo grandchild=$! >&2; wait' & echo child=$! >&2; wait", -1},
		{"echo driver=$$ >&2; sleep 30 & echo child=$! >&2; exit 0", -1},
		{"echo driver=$$ >&2; sleep 30 >/dev/null & echo child=$! >&2; exit 0", 0}};
	for (const auto& test : cases)
	{
		const auto start = steady_clock::now();
		const auto answer = run(test.first, milliseconds(100));
		assert(answer.code == test.second);
		const auto elapsed = duration_cast<milliseconds>(steady_clock::now() - start).count();
		assert(elapsed < 3000);
		std::cout << "case rc=" << answer.code << " elapsed_ms=" << elapsed << std::endl;
		// Child's parent exited, so each killed descendant is ours to reap.
		// Bound the proof itself: any live descendant is a failing test.
		const auto deadline = steady_clock::now() + seconds(2);
		while (true)
		{
			int status;
			const pid_t pid = waitpid(-1, &status, WNOHANG);
			if (pid > 0)
			{
				std::cout << "reaped pid=" << pid << std::endl;
				continue;
			}
			if (pid < 0 && errno == ECHILD)
				break;
			assert(steady_clock::now() < deadline);
			poll(nullptr, 0, 10);
		}
	}
	std::cout << "PASS: actual Wi-Fi runner process controls" << std::endl;
}
