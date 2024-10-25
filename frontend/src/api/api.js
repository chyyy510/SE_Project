import axiosInstance from './index'

const axios = axiosInstance

export const getBooks = () => 
    {return axios.get(`http://localhost:8080/api/books/`)}

export const postRegister = (email, username, password) => 
    {return axios.post(`http://localhost:8080/users/register/`, {'email': email, 'nickname': username, 'password_hashed': password})}