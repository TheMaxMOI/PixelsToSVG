from svg import SVG, Text, Tspan

valid = SVG(100, 100).setData([Text().setData(["hello", Tspan().setData(["nested"])])])

invalidList = [
    SVG(100, 100).setData([Tspan()]),
    SVG(100, 100).setData([Tspan().setData(["ouho", Tspan().setData(["inner"])])]),
]

assert valid.checkTspan()

for invalid in invalidList:
    assert not invalid.checkTspan()

try:
    invalidList[0].export()
    assert False
except SyntaxError as err:
    assert (
        f"{err}" == "Tspan instances must be children of other Tspan or Text instances!"
    )
