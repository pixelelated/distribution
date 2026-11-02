# T44 tool interface preflight

The helper and lint support `--help` and returned 0. `tools/box-check` does
not implement help: `--help` fell through to its read-only tracker path and
failed to connect in the restricted environment (rc1). Its actual single
issue interface is `tools/box-check --issue NUMBER`. `tools/forbidden-terms-check`
also has no help option: it treated `--help` as a directory and returned2;
its interfaces are a tree path or `--stdin`. Neither return is a gate PASS.
Use current normal record checks/hooks and the real single-issue interface.
An earlier preflight spelling `tools/issue-box-check` did not exist and
Python raised FileNotFoundError; it executed no checker. The source/interface
inspection corrected that name before brief publication or dispatch.
