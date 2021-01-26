import numpy as np

from timer import Timer

def null(A):
  e_vals, e_vecs = np.linalg.eigh(np.dot(A.T, A))  
  # extract the eigenvector (column) associated with the minimum eigenvalue
  return e_vecs[:, np.argmin(e_vals)]

def mean_coreset(P, u, eps = 1e-10):
  d = P.shape[1]
  if P.shape[0] <= d + 1:
    return (P, u)
  A = (P[1:] - P[0]).T
  v_n = null(A)
  v1 = np.atleast_1d(-1 * np.sum(v_n))
  v = np.concatenate((v1, v_n))
  non_zero = np.where(v > eps)
  alpha = np.min(np.divide(u[non_zero], v[non_zero]))
  w_all = u - (alpha * v)
  w_non = np.where(w_all > eps)
  S = P[w_non]
  w = w_all[w_non]
  if S.shape[0] > d + 1:
    S, w = mean_coreset(S, w)
  return S, w

def stream_coreset(data, stop_in = None):
  S = data[0].reshape((1, data.shape[1]))
  w = np.atleast_1d(1.0)
  
  time = np.zeros(data.shape[0])
  timer = Timer()
  stop = data.shape[0]
  if stop_in:
    stop = stop_in
  
  for i in range(2, stop):
    timer.start()
    
    q = data[i].reshape((1, data.shape[1]))
    P = np.concatenate((S, q))
    u_p = w * ((i - 1) / i)
    u = np.concatenate((u_p, np.atleast_1d(1 / i)))
    S, w = mean_coreset(P, u)
    
    elapsed = timer.stop()
    time[i] = elapsed
  
  return S, w, time



