
async function main() {
    try {
        const res = await fetch("https://jsonplaceholder.typicode.com/posts/1")
        if (!res.ok) {
            throw new Error("HTTPS ERROR")
        }
        const data = await res.json()
        console.log(res)
        console.log(data)
    }
    catch (error) {
        console.log(error.message)
    }
}

main()

