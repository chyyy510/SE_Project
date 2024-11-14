import axiosInstance from './index'

const axios = axiosInstance

export const getBooks = () => 
    {
        return axios.get(`http://10.7.67.55:8000/books/`),{withCredentials: true}
    }

export const postRegister = (email, username, password) => 
    {
        return axios.post(`http://10.7.67.55:8000/users/register/`, {'email': email, 'username': username, 'password_encrypted': password},
        {
            headers: { 'Content-Type': 'application/json',
                 
                } 
            },{withCredentials: true}) 
         .then(response => 
            { console.log(response.data); }) 
            .catch(error => { console.error('There was an error!', error); });
            
        }
export const user_login = (email, password) => 
            {
                return axios.post(`http://10.7.67.55:8000/users/login/`, {'email': email, 'password_encrypted': password},
                {
                    headers: { 'Content-Type': 'application/json',
                         
                        } 
                    },{withCredentials: true}) 
                 .then(response => 
                    {   const is_active=response.is_active;
                         if(!is_active)
                            console.log('登陆失败',response.data);
                        else{
                            const user_id=response.data.access;
                            const username=response.data.username;
                            const email=response.data.email;
                            console.log('登录成功:', { user_id, username, email })
                    }

                     }) 
                    .catch(error => { console.error('There was an error!', error); });
                    
                }