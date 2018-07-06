import axios from 'axios'

// const host = 'http://127.0.0.1:8888' //发布
const host = 'http://127.0.0.1:8000' //开发
const headers = {
    'X-CSRFToken': getCookie('csrftoken')
    // 'Cookie': 'csrftoken=' + getCookie('csrftoken')
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const service = axios.create({
    timeout: 10000,
    host: host,
    baseURL: host + '/api',
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: headers
})



export default service