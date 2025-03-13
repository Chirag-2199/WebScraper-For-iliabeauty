import { Route, Routes } from "react-router-dom"
import AuthLogin from "./pages/auth/login"
import AuthRegister from "./pages/auth/register"
import AuthLayout from "./components/auth/layout"; // you did not imported authlayout thats why its throwing the authlayout not defined error


function App() {


  return (
    <div className="flex flex-col overflow-hidden bg-white">

      <h1>header component</h1>

      <Routes>
        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={<AuthLogin />} />
          <Route path="register" element={<AuthRegister />} />

        </Route>
      </Routes>
    </div>
  )
}

export default App;
