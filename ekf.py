""" Written by Brian Hou for CSE571: Probabilistic Robotics (Winter 2019)
"""

import numpy as np

from utils import minimized_angle


class ExtendedKalmanFilter:
    def __init__(self, mean, cov, alphas, beta):
        self.alphas = alphas
        self.beta = beta

        self._init_mean = mean
        self._init_cov = cov
        self.reset()

    def reset(self):
        self.mu = self._init_mean
        self.sigma = self._init_cov

    def update(self, env, u, z, marker_id):
        """Update the state estimate after taking an action and receiving a landmark
        observation.

        u: action
        z: landmark observation
        marker_id: landmark ID
        """
        mu_flat = self.mu.ravel()
        u_flat = u.ravel()

        # --- Prediction Step ---
        G = env.G(mu_flat, u_flat)
        V = env.V(mu_flat, u_flat)
        M = env.noise_from_motion(u_flat, self.alphas)
        mu_bar = env.forward(mu_flat, u_flat)
        sigma_bar = G @ self.sigma @ G.T + V @ M @ V.T

        # --- Measurement Update Step ---
        z_hat = env.observe(mu_bar.ravel(), marker_id)
        innovation = minimized_angle(z[0, 0] - z_hat[0, 0])
        innovation = np.array([[innovation]])

        H = env.H(mu_bar, marker_id)
        S = H @ sigma_bar @ H.T + self.beta
        K = sigma_bar @ H.T @ np.linalg.inv(S)

        self.mu = (mu_bar + K @ innovation).reshape((-1, 1))
        self.mu[2, 0] = minimized_angle(self.mu[2, 0])
        self.sigma = (np.eye(3) - K @ H) @ sigma_bar

        return self.mu, self.sigma
