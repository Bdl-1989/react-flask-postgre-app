import React, { useState } from 'react'
import axios from 'axios';
import { Navigate } from 'react-router-dom';

export const Register = () => {
    const [username, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [navigate, setNavigate] = useState(false)

    const submit = async (e) => {
        e.preventDefault();
        await axios.post('/auth/register', {
            username,
            email,
            password
        })
        setNavigate(true);
    }

    // if (navigate) {
    //     window.location.href = '/login';
    // }
    if (navigate) {
        return <Navigate to="/login" />
    }

    return (
        <main className="form-signin w-100 m-auto">
            <form onSubmit={submit}>
                <img className="mb-4" src="/docs/5.3/assets/brand/bootstrap-logo.svg" alt="" width="72" height="57" />
                <h1 className="h3 mb-3 fw-normal">Please register</h1>
                <div className="form-floating">
                    <input type="text" className="form-control" id="floatingInput1" placeholder="Name"
                        onChange={e => setName(e.target.value)} />
                    <label htmlFor="floatingInput">Name</label>
                </div>
                <div className="form-floating">
                    <input type="email" className="form-control" id="floatingInput2" placeholder="name@example.com"
                        onChange={e => setEmail(e.target.value)} />
                    <label htmlFor="floatingInput">Email address</label>
                </div>
                <div className="form-floating">
                    <input type="password" className="form-control" id="floatingPassword" placeholder="Password"
                        onChange={e => setPassword(e.target.value)}
                    />
                    <label htmlFor="floatingPassword">Password</label>
                </div>

                <div className="form-check text-start my-3">
                    <input className="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault" />
                    <label className="form-check-label" htmlFor="flexCheckDefault">
                        Remember me
                    </label>
                </div>
                <button className="btn btn-primary w-100 py-2" type="submit">Submit</button>
                <p className="mt-5 mb-3 text-body-secondary">&copy; 2017-2024</p>
            </form>
        </main>
    )
}
