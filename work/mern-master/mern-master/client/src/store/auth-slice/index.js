import { createSlice } from "@reduxjs/toolkit"; // here you imported in wrong format you imported this as 'import { createSlice } from ("@reduxjs/toolkit")' which is wrong i guess

// const { User } = require("lucide-react");



const initialState = {
    isAuthenticated: false,
    isLoading: false,
    User: null
};



const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        setUser: (state, action) => { },
    },
});

export const { setUser } = authSlice.actions;
export default authSlice.reducer;