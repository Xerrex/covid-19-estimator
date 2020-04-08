from .covid19ImpactEstimator import days_calculator, \
	covid19ImpactEstimator


def estimator(data):

	# convert time to days
	timeToElapseInDays = days_calculator(data["periodType"], 
							data["timeToElapse"])

	# impact estimate
	impact = covid19ImpactEstimator(timeToElapseInDays, 
				data["reportedCases"])

	# 
	severeImpact = covid19ImpactEstimator(timeToElapseInDays,
				data["reportedCases"], impact="severe")

	data = {
		"data": data,
		"impact": impact,
		"severeImpact": severeImpact
	}
	return data
