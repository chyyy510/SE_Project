import axiosInstance from './index'

const axios = axiosInstance
const SERVER_URL = 'http://192.168.232.25:8000';

export const postLogin = (email, password) => {
  return axios.post(`${SERVER_URL}/users/login/`, { 'email': email, 'password_encrypted': password }), { withCredentials: true }
}

export const postRegister = (email, username, password) => {
  return axios.post(`${SERVER_URL}/users/register/`, { 'email': email, 'username': username, 'password_encrypted': password },
    {
      headers: {
        'Content-Type': 'application/json',

      }
    }, { withCredentials: true })
    .then(response => { console.log(response.data); })
    .catch(error => { console.error('There was an error!', error); });

}

export const postSearch = (title, description, orderby, sort) => {
  return axios.post(`${SERVER_URL}/experiments/search/?title=${title}&description=${description}&orderby=${orderby}&sort=${sort}`,
    {
      headers: {
        'Content-Type': 'application/json',

      }
    }, { withCredentials: true })
    .then(response => { console.log(response.data); })
    .catch(error => { console.error('There was an error!', error); });

}
