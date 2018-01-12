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
- [x] Format the metadata selection paragraph so it is readable / useful.
	- [x] Explore conversion into an ISA object.
	- [x] Move to the right hand side of the plot.
- [x] Filter the options available in the X and Y drop down selectors.
- [x] Add a color by drop down.
- [ ] Add more metadata information in the metadata div element.
	- [ ] NMR acquisition information.
	- [ ] Sample progeny information.
- [x] Add counter-ion functionality.
	- [x] Create the FactorValue instances for each Sample() instance.
	- [x] Create the counter_ion StudyFactor.
- [ ] Add a unique marker drop down.
- [ ] Add a log scale toggle.
- [ ] Create user-friendly strings for column names.
- [ ] Add a process element.
- [ ] Add more data points.
- [ ] Change theme or colors for visibility.

## TODO: Demo Presentation

- [ ] Prepare / update poster.
- [ ] Prepare ISA document diagram.

## TODO: Yak-shaving

- [ ] Update Bokeh layout elements by name, rather than nested indexes.
- [ ] Change the demo data generation to a function.