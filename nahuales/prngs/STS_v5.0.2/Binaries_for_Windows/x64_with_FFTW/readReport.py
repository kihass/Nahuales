from os.path import exists

def readReports(argPathSTS: str, argProof: str, argExt: str, argFile: str, argKey: str) -> str:
	"""Read the Statistical Test Suite (STS) reports and group them in Comma 
	Separated Values (CSV)
	
	argProof    Gets the name of the test that generated the report
	argFile     Gets the name of the file used to generate the sequence 
	            analyzed by the STS and from which the report was generated
	argExt      Gets the name of the file extension used to generate the 
	            sequence analyzed by the STS and from which the report was 
				generated
	argKey      Gets the key used to generate the sequence analyzed by the STS
	"""
	statsPath = '{}experiments/AlgorithmTesting/'.format(argPathSTS)
	output = ''
	finalScore = 0
	proof = [
			'Frequency',  # 1
			'BlockFrequency',  # 2
			'CumulativeSums',  # 3
			'Runs',  # 4
			'LongestRun',  # 5
			'Rank',  # 6
			'FFT',  # 7
			'NonOverlappingTemplate',  # 8
			'OverlappingTemplate',  # 9
			'Universal',  # 10
			'ApproximateEntropy',  # 11
			'RandomExcursions',  # 12
			'RandomExcursionsVariant',  # 13
			'Serial',  # 14
			'LinearComplexity',  # 15
			]

	for dirName in proof:
		fn = '{}/{}/stats.txt'.format(statsPath, dirName)
		cntSuccess = 0
		cntFailure = 0
		cntValues = 0
		lstPValues = []
		
		if not exists(fn):
			continue

		with open(fn, mode='r') as file:
			while True:
				buffer = file.readline()

				if not buffer:
					break

				buffer = buffer.strip()

				if 'SUCCESS' in buffer:
					cntSuccess += 1

				elif 'FAILURE' in buffer:
					cntFailure += 1

				if ('\tp_value = ' in buffer
						or ' p_value = ' in buffer
						or ' p-value = ' in buffer
						or '\tp_value1 = ' in buffer
						or '\tp_value2 = ' in buffer):
					pValue = float(buffer[-8:])
					lstPValues.append(pValue)

				elif (buffer[-6:].isdigit() and '.' == buffer[-7:-6]
						and not '=' in buffer):
					pValue = float(buffer[-8:])
					lstPValues.append(pValue)

					if pValue > 0.01:
						cntSuccess += 1

					else:
						cntFailure += 1

				elif 'SUCCESS' in buffer[-8:] or 'FAILURE' in buffer[-8:]:
					# print(buffer[-15:-8])
					pValue = float(buffer[-15:-8])
					lstPValues.append(pValue)

				elif len(buffer) == 80:
					pValue = float(buffer[60:69])
					lstPValues.append(pValue)

		# print(dirName, lstPValues)
		cntValues = cntSuccess + cntFailure
		score = round(cntSuccess / cntValues, 2)
		# print(score)
		finalScore += score
		pValueAverage = round(sum(lstPValues) / float(len(lstPValues)),2)
		output += ',{},{}'.format(pValueAverage, score)

	output = '{},{},{},{},'.format(argProof, argExt, argFile, argKey) \
			+ '{}{}'.format(finalScore, output)

	return output


if __name__ == '__main__':
	readReports('', 'test','file','ext','key')
