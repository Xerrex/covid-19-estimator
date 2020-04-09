#!/usr/bin/python3

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

data_expected = {
    data: {}, # the input data you got
    impact: {}, your best case estimation
    severeImpact: {} #your severe case esitmation
}
"""


def days_calculator(periodType, period):
  """Calculates days from period and the period type 
  provided in arguements.
  
  It assumes a month has 30 days.

  Arguments:
    - periodType {str:String} 
        -- type in which period is provided ie. days, weeks, months

    - period {int:Integer} -- numeric value of the quantity of time.
  
  Returns:
    - int:Integer -- the number of days 
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


def covid19ImpactEstimator(impact, timeToElapseInDays, **data):
  """Calculate the covid 19 estimates

  Assumptions:
    - Infections double every 3 days.
    - 15% severe positive cases require hospitalization to recover.
    - 35% bed availability in hospitals for severe.
    - 5%  of infections cases require ICU.

  Arguments:
    - impact {int: integer} -- value to multiply reported cases 
        as per scenario ie. best_case or worstcase
    - timeToElapseInDays {int: integer} -- number of days for the estimate.

  Keyword Arguments:
    - reportedCases {int:integer} -- number of positive cases.
    - avgDailyIncomeInUSD {numeric} --the average daily income in USD.
    - avgDailyIncomePopulation {numeric} -- Average Daily Income Population.
    - totalHospitalBeds {int:Integer} -- total available Hospital Beds.

  Returns:
    - dict() -- values for the Novel covid-19
  """
  
  multiplier = 2 ** int(timeToElapseInDays / 3)
  expectedHospitalBeds = data["totalHospitalBeds"] * 0.35
  aDIIU = data["avgDailyIncomeInUSD"]
  aDIP = data["avgDailyIncomePopulation"]


  cI = data["reportedCases"] * impact
  iBRT = cI * multiplier
  sCBRT = iBRT * 0.15
  hBBRT = expectedHospitalBeds - sCBRT
  cFICUBRT = iBRT * 0.05,
  cFVBRT = iBRT * 0.02
  dollarsInFlight = iBRT* timeToElapseInDays * aDIIU * aDIP

  return {
      "currentlyInfected": cI,
      "infectionsByRequestedTime": iBRT,
			"severeCasesByRequestedTime": sCBRT,
      "hospitalBedsByRequestedTime":  hBBRT,
      "casesForICUByRequestedTime": cFICUBRT,
      "casesForVentilatorsByRequestedTime": cFVBRT,
      "dollarsInFlight": dollarsInFlight
    } 

