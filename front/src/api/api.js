import axiosInstance from './index'

const axios = axiosInstance

export const getBooks = () => 
    {return axios.get(`http://localhost:8000/api/user/`)}

export const postRegister = (email, username, password) => 
    {return axios.post(`http://localhost:8000/api/user/`, {'email': email, 'username': username, 'password_encrypted': password})}