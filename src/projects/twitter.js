import React, {useState} from 'react'

import axios from 'axios';
const TwitterProject =()=>{
    const [words, setWords] = useState("hello")
    const [answer, setAns]  = useState(null)
    return(
        <div>
        <h1>{words}</h1>
        <form onSubmit={(e)=>{
            e.preventDefault()
            const payload={
                w:words
            }
            axios 
            .post('http://localhost:5000/t', {
            headers: { "Access-Control-Allow-Origin": "*" },
            body: words
        },payload
            )
            
            .then((res)=>{
                console.log(res)
                setAns(res.data)
            }).catch((error)=>{
                console.log(error)
            })
        }}
            >
            <label htmlFor="textbox">
            <input id="box" value={words} name = 'search'
            placeholder="type something" onChange={e=>setWords(e.target.value)}/>
            </label>
            <button>submit</button>
        </form>
        <p id='val' >{answer}</p>
        
        </div>
    )
}

export default TwitterProject