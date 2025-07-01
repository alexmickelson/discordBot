import axios from "axios";
import { toast } from "react-hot-toast";

// Create an Axios instance
const axiosClient = axios.create({});

// Add a response interceptor for global error handling
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    let message = "An error occurred";
    if (error.response && error.response.data && error.response.data.detail) {
      message = error.response.data.detail;
    } else if (error.response && error.response.statusText) {
      message = error.response.statusText;
    } else if (error.message) {
      message = error.message;
    }
    toast.error(message);
    return Promise.reject(error);
  }
);

export default axiosClient;
