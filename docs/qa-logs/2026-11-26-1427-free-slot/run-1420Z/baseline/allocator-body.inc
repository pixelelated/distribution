int SaveStateRepository::getNextFreeSlot(FileData* game, std::shared_ptr<SaveStateConfig> config)
{
	if (!isEnabled(game))
		return -99;

	auto repo = game->getSourceFileData()->getSystem()->getSaveStateRepository();	
	auto states = repo->getSaveStates(game, config);

	if (states.size() == 0)
		return config != nullptr ? config->firstslot : 0;

	for (int i = 99999; i >= 0; i--)
	{
		auto it = std::find_if(states.cbegin(), states.cend(), [i](const SaveState* x) { return x->slot == i; });
		if (it != states.cend())
			return i + 1;
	}

	return -99;
}
