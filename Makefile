.PHONY: test quick

quick:
	PYTHONPATH=src python analysis/01_titi_2013_reanalysis.py
	PYTHONPATH=src python analysis/02_bert2019_reanalysis.py
	PYTHONPATH=src python analysis/03_vervet_2023_channelA.py
	PYTHONPATH=src python analysis/04_mangabey_2022_channelC.py --permutations 10000
	PYTHONPATH=src python analysis/05_vervet_2022_channelC.py

test:
	PYTHONPATH=src python tests/smoke_test.py
