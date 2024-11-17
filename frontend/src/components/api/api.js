import axiosInstance from './index'

const axios = axiosInstance

export const postLogin = () => 
    {
        return axios.get(`http://10.7.67.55:8000/users/register/`),{withCredentials: true}
    }

export const postRegister = (email, username, password) => 
    {
        return axios.post(`http://192.168.244.25:8000/users/register/`, {'email': email, 'username': username, 'password_encrypted': password},
        {
            headers: { 'Content-Type': 'application/json',
                 
                } 
            },{withCredentials: true}) 
         .then(response => 
            { console.log(response.data); }) 
            .catch(error => { console.error('There was an error!', error); });
            
        }