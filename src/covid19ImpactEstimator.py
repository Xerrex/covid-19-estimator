"""COVID-19 Impact Estimator


data_provided = {
    "region":{
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 5,
        "avgDailyIncomePopulation": 0.71
    },
    "periodType":"days",
    "timeToElapse": 58,
    "reportedCases": 674,
    "population": 66622705,
    "totalHospitalBeds": 1389614
}

estimated_values = {
    data: {},
    impact: {
        "currentlyInfected": reportedCases*10,
        "infectionsByRequestedTime": "currentlyInfected x (2 to the power of int(days/3))",
    }, 
    severeImpact: {
        "currentlyInfected": reportedCases*50,
        "infectionsByRequestedTime": "currentlyInfected x (2 to the power of int(days/3))",
    } #your severe case esitmation
}
"""


def days_calculator(periodType, period):
    """Calculates days from period and the period type 
    provided in arguements.
    
    It assumes a month has 30 days.

    Arguments:
        periodType {str:String} 
            -- type in which period is provided ie. days, weeks, months

        period {int:Integer} -- numeric value of the quantity of time.
    
    Returns:
        int:Integer -- the number of days 
    """

    if periodType == "days":
        days = period
    elif periodType == "weeks":
        days = period * 7
    elif periodType == "months":
        days = period * 30
    else:
        return None
    
    return int(days)


def covid19ImpactEstimator(timeToElapseInDays, reportedCases, totalHospitalBeds, impact=None):
    """Calculates the impact per estimates

    Asssumtions:\n
      1. At best that currently infected persons are
        reportedCases * 10 
      2. At Severe that currenlty infected persons are
        reportedCases * 50
      3. Infections double every 3 days
		  4. 15% severe positive cases require hospitalization to recover 
		  5. 35% bed availability in hospitals for severe 
			  COVID-19 positive patients.

    Arguments:

      timeToElapseInDays {int:Integer} -- number of days for the estimate
      reportedCases {int:Integer} -- the number of reported infected cases
      totalHospitalBeds {int:Integer} -- number of avaialbe hospital beds

    Keyword Arguments:

      impact {str:string} -- the impact to esitmate (default: {None})

    Returns:

        dict(): Dictionary -- contains the keys 'currentlyInfected'
            'infectionsByRequestedTime' an their values
    """
    
    factor = int(timeToElapseInDays / 3)
    multiplier = 2 ** factor
    expectedHospitalBeds = int(totalHospitalBeds * 0.35)

    if impact == None:
      currentlyInfected = reportedCases * 10
      infectionsByRequestedTime = currentlyInfected * multiplier
      severeCasesByRequestedTime = infectionsByRequestedTime * 0.15
      hospitalBedsByRequestedTime = expectedHospitalBeds - severeCasesByRequestedTime

    elif impact == "severe":
      currentlyInfected = reportedCases * 50
      infectionsByRequestedTime = currentlyInfected * multiplier
      severeCasesByRequestedTime = int(infectionsByRequestedTime * 0.15)
      hospitalBedsByRequestedTime = expectedHospitalBeds - severeCasesByRequestedTime

    return {
      "currentlyInfected": currentlyInfected,
      "infectionsByRequestedTime": infectionsByRequestedTime,
			"severeCasesByRequestedTime": severeCasesByRequestedTime,
      "hospitalBedsByRequestedTime":  hospitalBedsByRequestedTime
    } 
