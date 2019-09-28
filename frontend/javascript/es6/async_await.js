const person = function (name, year) {
    return new Promise((resolve, reject) =>
        setTimeout(resolve, 500, [name, year])
    );
};

const age = function (year) {
    return new Promise((resolve, reject) =>
        setTimeout(resolve, 500, `The age is ${new Date().getFullYear() - year}`)
    );
};


async function getAge() {
    const [n, y] = await person('Rohit', 1986);
    const res = await age(y);
    return res;

};


getAge().then(res => console.log(res));
