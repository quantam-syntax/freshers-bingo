import { createContext, useState, useEffect, useContext } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [role, setRole] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    const savedRole = localStorage.getItem('role')
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
      setRole(savedRole)
    }
    setLoading(false)
  }, [])

  function loginFresher(fresherData, jwtToken) {
    setUser(fresherData)
    setToken(jwtToken)
    setRole('fresher')
    localStorage.setItem('token', jwtToken)
    localStorage.setItem('user', JSON.stringify(fresherData))
    localStorage.setItem('role', 'fresher')
  }

  function loginAdmin(adminData, jwtToken) {
    setUser(adminData)
    setToken(jwtToken)
    setRole('admin')
    localStorage.setItem('token', jwtToken)
    localStorage.setItem('user', JSON.stringify(adminData))
    localStorage.setItem('role', 'admin')
  }

  function logout() {
    setUser(null)
    setToken(null)
    setRole(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('role')
  }

  return (
    <AuthContext.Provider value={{
      user, token, role, loading,
      isAuthenticated: !!token,
      isFresher: role === 'fresher',
      isAdmin: role === 'admin',
      loginFresher, loginAdmin, logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

export default AuthContext
