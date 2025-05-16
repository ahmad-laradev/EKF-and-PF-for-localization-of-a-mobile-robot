# EKF and PF for Localization of a Mobile Robot

This project is about implementing and comparing two important filters used in mobile robot localization: the Extended Kalman Filter (EKF) and the Particle Filter (PF). Both filters are used to estimate the robot’s position and orientation while it moves in a 2D world with noise in both its actions and its observations.

We worked in Python and tested the filters in a simple simulated environment using noisy control inputs and landmark-based observations.

## Project Structure

- `ekf.py`: Our implementation of the Extended Kalman Filter.
- `pf.py`: Our implementation of the Particle Filter, including low-variance resampling.
- `soccer_field.py`: The simulation environment with landmark definitions, motion and observation models, and noise settings.
- `utils.py`: Helper functions for plotting and angle normalization.
- `localization.py`: The main script to run the simulation and apply the filters.
- `run_experiments.py`: A script to automate experiments and collect results.

## How to Run

To simulate the robot and see the filter estimates in action, you can run:

```bash
python localization.py --plot --filter-type ekf
python localization.py --plot --filter-type pf
python localization.py --plot --filter-type none
```

To check all available options:

```bash
python localization.py -h
```

## Input Format

- **State**: `[x, y, θ]` — robot’s position and orientation.
- **Control**: `[δrot1, δtrans, δrot2]` — turn, move, turn again.
- **Observation**: `[θ_bearing]` — angle to a visible landmark.

## Notes

- Always use `utils.minimized_angle()` to keep angles between -π and π.
- The PF uses low-variance resampling for better performance.
- For large experiments, we recommend turning off plotting to save time.

## What We Did

We implemented both filters from scratch, tested them under different levels of noise, and compared their performance. We measured the accuracy using position error, ANEES, and Mahalanobis error. For the Particle Filter, we also checked how the number of particles affects the results.

The EKF worked well in low-noise settings, while the PF handled more difficult situations better. PF needs more particles to work well and runs slower, but it's more flexible overall.

This project helped us understand how filtering works for localization in robotics, especially when dealing with real-world uncertainty.

## References

- Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
- Class slides and TP4 instructions
- NumPy and Matplotlib official docs