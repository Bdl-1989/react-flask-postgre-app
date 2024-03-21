import React, { useState } from 'react'
import axios from 'axios';
import { Navigate } from 'react-router-dom';

export const Login = () => {
    const [username, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [navigate, setNavigate] = useState(false)

    const submit = async (e) => {
        e.preventDefault();
        const {data} = await axios.post('/auth/login', {
            username,
            password
        }, {
            withCredentials: true
        })
        console.log(data['token']['access_token']);

        axios.defaults.headers.common['Authorization'] = `Bearer ${data['token']['access_token']}`
        setNavigate(true);
    }

    // if (navigate) {
    //     window.location.href = '/login';
    // }
    if (navigate) {
        return <Navigate to="/home" />
    }

    return (
        <main className="form-signin w-100 m-auto">
            <form onSubmit={submit}>
                <img className="mb-4" alt="" width="72" height="57" />
                <h1 className="h3 mb-3 fw-normal">Please sign in</h1>

                <div className="form-floating">
                    <input type="text" className="form-control" id="floatingInput" placeholder="username"
                        onChange={e => setName(e.target.value)} />
                    <label htmlFor="floatingInput">User Name</label>
                </div>
                <div className="form-floating">
                    <input type="password" className="form-control" id="floatingPassword" placeholder="Password"
                        onChange={e => setPassword(e.target.value)} />
                    <label htmlFor="floatingPassword">Password</label>
                </div>

                <div className="form-check text-start my-3">
                    <input className="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault" />
                    <label className="form-check-label" htmlFor="flexCheckDefault">
                        Remember me
                    </label>
                </div>
                <button className="btn btn-primary w-100 py-2" type="submit">Sign in</button>
                <p className="mt-5 mb-3 text-body-secondary">&copy; 2017-2024</p>
            </form>
        </main>
    )
}
