import { error } from 'shelljs';
import Header from '../Header.vue';
import axiosInstance from './index'

const axios = axiosInstance
const SERVER_URL = 'http://192.168.232.25:8000';

export const postLogin = (email, password) => 
    {
        return axios.post(`${SERVER_URL}/users/login/`, 
                        {'email': email, 'password_encrypted': password},
                        {withCredentials: true});
    }

export const postRegister = (email, username, password) => 
    {
        return axios.post(`${SERVER_URL}/users/register/`, 
                        {'email': email, 'username': username, 'password_encrypted': password},
                        {withCredentials: true});
    }

export const getSearch = (key, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/experiments/search/?keyword=${key}&orderby=${orderby}&sort=${sort}`,
                        {withCredentials: true});            
    }

export const getLaunchSearch = (access, key, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/experiments/create/search/?keyword=${key}&orderby=${orderby}&sort=${sort}`,
                        {headers: {'Authorization':`Bearer ${access}`}},
                        {withCredentials: true});            
    }  

export const getApplySearch = (access, key, orderby, sort) => 
    {
        return axios.get(`${SERVER_URL}/relations/engage/search/?keyword=${key}&orderby=${orderby}&sort=${sort}`,
                        {headers: {'Authorization':`Bearer ${access}`}},
                        {withCredentials: true});            
    }  

export const getApplier = (access, experiment) => 
    {
        return axios.get(`${SERVER_URL}/relations/volunteer/list/?experiment=${experiment}`,
                        {headers: {'Authorization':`Bearer ${access}`}},
                        {withCredentials: true});            
    }  
export const getTag = () => 
    {
        return axios.get(`${SERVER_URL}/relations/tags`,
                        {withCredentials: true});             
    }

export const postApply = (access, experiment) => 
    {
        return axios.post(`${SERVER_URL}/relations/engage/`,
                        {"experiment": experiment},
                        {headers: {'Authorization':`Bearer ${access}`}},
                        {withCredentials: true});             
    }

export const postQualify = (name, description) => 
    {
        return axios.post(`${SERVER_URL}/experiments/search/?title=${title}&description=${description}&orderby=${orderby}&sort=${sort}`,
                        {withCredentials: true});             
    }

export const getProject = (id) => 
    {
            return axios.get(`${SERVER_URL}/experiments/${id}/`,
                            {withCredentials: true});        
    }

export const getUser = (id) => 
    {
        return axios.get(`${SERVER_URL}/users/${id}/`,
                        {withCredentials: true});        
    }
export const updateUserInfo = (access, userInfo) => 
    { 
        console.log(userInfo);
        return axios.post(`${SERVER_URL}/users/profile/edit/`, userInfo, 
            {headers: {'Authorization':`Bearer ${access}`}},
            { withCredentials: true }); 
    }
export const updateUserPassword = (access, oldPassword,newPassword) => 
    { 
        console.log(access,oldPassword,newPassword);
        return axios.post(`${SERVER_URL}/users/profile/edit/`, oldPassword,newPassword, 
            {headers: {'Authorization':`Bearer ${access}`}},
            { withCredentials: true }); 
    }
    
export const postProject = (access, mode, id, title, activity_time, activity_location, person_wanted, money_per_person, description) => 
    {
        return axios.post(`${SERVER_URL}/experiments/${mode}/`, 
                        {'id': id, 'title': title, 'activity_time': activity_time, 'activity_location': activity_location, 
                        'person_wanted': person_wanted, 'money_per_person': money_per_person, 'description': description},
                        {headers: {'Authorization':`Bearer ${access}`}},
                        {withCredentials: true});
    }