import React, {useState} from 'react'

const Content =()=>{
    const [words, setWords] = useState("hello")
    return(
        <div>
        <h1>{words}</h1>
        <form onSubmit={(e)=>{
            e.preventDefault()
            alert(words)
        }}>
            <label htmlFor="textbox">
            <textarea id="box" value={words}
            placeholder="type something" onChange={e=>setWords(e.target.value)}/>
            </label>
            <button>submit</button>
        </form>
        </div>
    )
}

export default Content