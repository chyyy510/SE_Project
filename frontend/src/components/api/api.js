import axiosInstance from './index'

const axios = axiosInstance
const SERVER_URL = 'http://192.168.244.25:8000';

export const postLogin = () => 
    {
        return axios.get(`${SERVER_URL}/users/register/`),{withCredentials: true}
    }

export const postRegister = (email, username, password) => 
    {
        return axios.post(`${SERVER_URL}/users/register/`, {'email': email, 'username': username, 'password_encrypted': password},
        {
            headers: { 'Content-Type': 'application/json',
                 
                } 
            },{withCredentials: true}) 
         .then(response => 
            { console.log(response.data); }) 
            .catch(error => { console.error('There was an error!', error); });
            
        }

export const postSearch = (email, username, password) => 
            {
                return axios.post(`${SERVER_URL}/users/register/`, {'email': email, 'username': username, 'password_encrypted': password},
                {
                    headers: { 'Content-Type': 'application/json',
                         
                        } 
                    },{withCredentials: true}) 
                 .then(response => 
                    { console.log(response.data); }) 
                    .catch(error => { console.error('There was an error!', error); });
                    
                }