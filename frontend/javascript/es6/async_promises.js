// const p1 = new Promise((resolve, reject) => setTimeout(resolve, 1000, 'Hello World'));
// const p2 = Promise.resolve("Hello Promises in ES6 !");
//
// p1.then(res => console.log(res));
// Promise.all([p1, p2]).then(res => console.log(res));

const person = function (name, year) {
    return new Promise((resolve, reject) =>
        setTimeout(resolve, 500, year)
    );
};

const age = function (year) {
    return new Promise((resolve, reject) =>
        setTimeout(resolve, 500, `The age is ${new Date().getFullYear() - year}`)
    );
};

person('Rohit', 1986)
    .then(res => age(res))
    .then(res => console.log(res));
