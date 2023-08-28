from Math import *

# Returns the slope, intercept, and form of the regression (if vertical or not)
def leastSquaresRegression(data):
    VERTICAL_LINE_THRESHOLD = 10
    averageX, averageY = averageXY(data)
    if averageSlope(Point(-1, -1), data) > VERTICAL_LINE_THRESHOLD: # Vertical Line
        slope = calculateRegressionSlope(data, True)
        intercept = averageX - slope * averageY
        return slope, intercept, True
    else:
        slope = calculateRegressionSlope(data, False)
        intercept = averageY - slope * averageX
        return slope, intercept, False

def calculateRegressionSlope(data, isVertical):
    averageX, averageY = averageXY(data)
    numerator = 0
    denominator = 0
    if isVertical:
        for i in data:
            numerator += (data[i].y - averageY) * (data[i].x - averageX)
            denominator += (data[i].y - averageY) ** 2
    else:
        for i in data:
            numerator += (data[i].x - averageX) * (data[i].y - averageY)
            denominator += (data[i].x - averageX) ** 2
    return numerator/denominator