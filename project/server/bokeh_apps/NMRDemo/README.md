# NMR Demo

**Requires an installation of isaDream**.

## Simple Deployment

This can be deployed in a standalone fashion for testing by running the bokeh serve command from within parent directory of NMRDemo.

```
bokeh serve NMRDemo/
```

## TODO

- [x] Add a title div.
- [x] Add a plot / figure title that updates according to the selections.
- [ ] Format the metadata selection paragraph so it is readable / useful.
	- [x] Explore conversion into an ISA object.
	- [x] Move to the right hand side of the plot.
- [ ] Filter the options available in the X and Y drop down selectors.
- [ ] Create user-friendly strings for column names.
- [ ] Add counter-ion functionality.
- [ ] Add a color by drop down.
- [ ] Add a unique marker drop down.
- [ ] Add more data points.
- [ ] Add a log scale toggle.
- [ ] Add a process element.

## TODO: Demo Presentation

- [ ] Prepare / update poster.
- [ ] Prepare ISA document diagram.

## TODO: Yak-shaving

- [ ] Update Bokeh layout elements by name, rather than nested indexes.
- [ ] Change the demo data generation to a function.