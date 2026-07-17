import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const getCourses = () => api.get("/courses/");
export const getCourse = (id) => api.get(`/courses/${id}`);
export const searchCourses = (q, n = 3) =>
  api.get(`/search/?q=${encodeURIComponent(q)}&n=${n}`);
export const getRecommendations = (completed) =>
  api.post("/recommend/", { completed });
export const getMissingPrereqs = (target, completed) =>
  api.post("/recommend/missing", { target, completed });
export const checkGraduation = (completed) =>
  api.post("/graduation/check", { completed });
export const getAdvice = (goal, completed) =>
  api.post("/advise/", { goal, completed });

export default api;
