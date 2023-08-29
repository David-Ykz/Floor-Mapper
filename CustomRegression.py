from Math import *

# Returns the slope, intercept, and form of the regression (if vertical or not)
def leastSquaresRegression(data):
    VERTICAL_LINE_THRESHOLD = 10
    averageX, averageY = averageXY(data)
    if abs(averageSlope(Point(-1, -1), data)) > VERTICAL_LINE_THRESHOLD and 0 == 1: # Vertical Line
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
        for point in data:
            numerator += (point.y - averageY) * (point.x - averageX)
            denominator += (point.y - averageY) ** 2
    else:
        for point in data:
            numerator += (point.x - averageX) * (point.y - averageY)
            denominator += (point.x - averageX) ** 2
    return numerator/denominator