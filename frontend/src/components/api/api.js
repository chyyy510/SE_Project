import axiosInstance from './index'

const axios = axiosInstance
const SERVER_URL = 'http://10.129.241.57:8080';

export const postLogin = (email, password) => 
    {
        return axios.post(`${SERVER_URL}/users/login/`, 
                        {'email': email, 'password': password},
                        {withCredentials: true})
                        .then(response => 
                            { console.log(response.data.error); }) 
                        .catch(error => { 
                            alert(response.data);
                            console.error(response.data); });
    }

export const postRegister = (email, username, password) => 
    {
        return axios.post(`${SERVER_URL}/users/register/`, 
                        {'email': email, 'username': username, 'password_encrypted': password},
                        {withCredentials: true}) 
                        .then(response => 
                            { console.log(response); }) 
                        .catch(error => { 
                            alert(response.data);
                            console.error(response.data); });
    }

export const getUser = (title, description, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/experiments/search/?title=${title}&description=${description}&orderby=${orderby}&sort=${sort}`,
                        {withCredentials: true}) 
                        .then(response => 
                            { console.log(response.data); }) 
                        .catch(error => { console.error('There was an error!', error); });             
    }

export const getSearch = (title, description, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/experiments/search/?title=${title}&description=${description}&orderby=${orderby}&sort=${sort}`,
                        {withCredentials: true}) 
                        .then(response => 
                        { console.log(response.data); }) 
                        .catch(error => { console.error('There was an error!', error); });             
    }

export const getTag = (title, description, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/experiments/search/?title=${title}&description=${description}&orderby=${orderby}&sort=${sort}`,
                        {withCredentials: true}) 
                        .then(response => 
                            { console.log(response.data); }) 
                        .catch(error => { console.error('There was an error!', error); });             
    }
export const postLaunch = (title, description, person_wanted, money_per_person) => 
    {
        return axios.post(`${SERVER_URL}/experiments/create`, {'title': title, 'description': description, 'person_wanted': person_wanted, 'money_per_person': money_per_person},
                        {withCredentials: true}) 
                        .then(response => 
                        { console.log(response.data); }) 
                        .catch(error => { console.error('There was an error!', error); });
    }