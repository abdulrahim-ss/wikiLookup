var t = null;

async function test1() {
    return new Promise( resolve => {
        const bruh = () => {
            if (t != null) {resolve(t);}
            else {
                setTimeout(bruh, 20);
            }
        }
        bruh();
    })
}

async function test2() {
    setTimeout(() => {t = "success";
    console.log("test2 ", t)}, 3000)
}

async function sui() {
    await test1();
    console.log("sui ", t);
}

test2()
sui()
