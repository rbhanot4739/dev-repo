class Element {
    constructor(name, buildYear) {
        this.name = name;
        this.buildYear = buildYear;
    }
}

class Park extends Element {
    constructor(name, buildYear, area, numTrees) {
        super(name, buildYear);
        this.area = area;
        this.numTrees = numTrees;
    }

    density() {
        return this.numTrees / this.area
    }
}

class Street extends Element {
    constructor(name, buildYear, length) {
        super(name, buildYear);
        this.length = length;
    }
}

let [parks, streets] = [[], []];
p1 = new Park("Park 1", 1990, 1024, 3000);
p2 = new Park("Park 2", 1940, 1024, 15000);
p3 = new Park("Park 3", 1965, 1024, 10000);
p4 = new Park("Park 4", 2002, 1024, 1000);

parks.push(p1, p2, p3, p4);

for (let p of parks) {
    console.log(`${p.name} has a density of ${p.density()}`);
}

parks.forEach(p => {
    console.log(`${p.name} has a density of ${p.density()}`);
});
