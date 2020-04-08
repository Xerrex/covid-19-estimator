from .covid19ImpactEstimator import days_calculator, \
	covid19ImpactEstimator


def estimator(data):

	# convert time to days
	timeToElapseInDays = days_calculator(data["periodType"], 
							data["timeToElapse"])

	# Unpack data
	aDIIU = data["region"]["avgDailyIncomeInUSD"]
	aDIP = data["region"]["avgDailyIncomePopulation"]
	reportedCases = data["reportedCases"]
	totalHospitalBeds = data["totalHospitalBeds"]

	# impact estimate
	best_case_estimation = covid19ImpactEstimator(10, timeToElapseInDays, 
					reportedCases=reportedCases, totalHospitalBeds=totalHospitalBeds, 
					avgDailyIncomeInUSD=aDIIU, avgDailyIncomePopulation=aDIP)

	# severe impact estimate
	worst_case_estimation = covid19ImpactEstimator(50, timeToElapseInDays, 
					reportedCases=reportedCases, totalHospitalBeds=totalHospitalBeds, 
					avgDailyIncomeInUSD=aDIIU, avgDailyIncomePopulation=aDIP)

	data = {
		"data": data,
		"impact": best_case_estimation,
		"severeImpact": worst_case_estimation
	}
	return data
