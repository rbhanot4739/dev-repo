function person(name) {
    setTimeout(function (n) {
        console.log('Hello ! my name is ' + n);
        const age = 33;
        setTimeout(function (a, n) {
            console.log(n + ' is ' + a + ' years old');
            setTimeout(function () {
                console.log('This is the final callback');
            }, 1500);
        }, 1500, age, name);
    }, 2000, name);

}


console.log('Started main...');
person('Rohit');
console.log("Finishing main.. but async code is still running in the background");
