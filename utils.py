from cil.optimisation.utilities import AlgorithmDiagnostics
import numpy as np
from bm3d import bm3d, BM3DStages
from cil.optimisation.functions import Function

class StoppingCriterionTime(AlgorithmDiagnostics):

    def __init__(self, time):

        self.time = time
        super(StoppingCriterionTime, self).__init__(verbose=0)

        self.should_stop = False
        
    def _should_stop(self):

        return self.should_stop       
            
    def __call__(self, algo):

        if algo.iteration==0:
            algo.should_stop = self._should_stop  

        stop_crit = np.sum(algo.timing)>self.time
        if stop_crit:
            self.should_stop = True                 
            print("Stop at {} time {}".format(algo.iteration, np.sum(algo.timing)))


class BM3DFunction(Function):
    """
    PnP 'regulariser' whose proximal applies BM3D denoising.

    In PnP-ISTA/FISTA we typically use a FIXED BM3D sigma (regularization strength),
    independent of the gradient step-size tau.
    Optionally apply damping: (1-gamma) z + gamma * BM3D(z).
    """

    def __init__(self, sigma, gamma=1.0, profile="np",
                 stage_arg=BM3DStages.ALL_STAGES, positivity=True):
        self.sigma = float(sigma)      # BM3D noise parameter
        self.gamma = float(gamma)      # damping in (0,1]
        if not (0.0 < self.gamma <= 1.0):
            raise ValueError("gamma must be in (0,1].")
        self.profile = profile
        self.stage_arg = stage_arg
        self.positivity = positivity
        super().__init__()

    def __call__(self, x):
        return 0.0

    def convex_conjugate(self, x):
        return 0.0

    def _denoise(self, znp: np.ndarray) -> np.ndarray:
        z = np.asarray(znp, dtype=np.float32)
        # BM3D expects sigma as noise std (same units as the image)
        return bm3d(z, sigma_psd=self.sigma,
                    profile=self.profile,
                    stage_arg=self.stage_arg).astype(np.float32)

    def proximal(self, x, tau, out=None):
        z = x.array.astype(np.float32, copy=False)
        d = self._denoise(z)

        # damping/relaxation (recommended if you see oscillations)
        u = (1.0 - self.gamma) * z + self.gamma * d

        if self.positivity:
            u = np.maximum(u, 0.0)

        if out is None:
            out = x * 0.0
        out.fill(u)
        return out


def create_circular_mask(h, w, center=None, radius=None):

    if center is None: 
        center = (int(w/2), int(h/2))
    if radius is None: 
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask


class StoppingCriterion(AlgorithmDiagnostics):
    def __init__(self, epsilon, epochs=None):
        self.epsilon = epsilon
        self.epochs = epochs
        super().__init__(verbose=0)
        self.should_stop = False
        self.rse_reached = False

    def _should_stop(self):
        return self.should_stop

    def __call__(self, algo):

        if algo.iteration == 0:
            algo.should_stop = self._should_stop

        stop_rse = (algo.rse[-1] <= self.epsilon)

        stop_epochs = False
        if self.epochs is not None:
            try:
                dp = algo.f.data_passes
                dp_last = dp[-1] if hasattr(dp, "__len__") else dp
                stop_epochs = (dp_last > self.epochs)
            except AttributeError:
                stop_epochs = False  
                
        stop = stop_rse or stop_epochs

        if algo.iteration < algo.max_iteration:
            if stop:
                self.rse_reached = stop_rse
                self.should_stop = True
                print(f"Accuracy reached at {algo.iteration}, time = {np.sum(algo.timing):.4f}, NRSE = {algo.rse[-1]:.4e}")
        else:
            print(f"Failed to reach accuracy. Stop at {algo.iteration}, time = {np.sum(algo.timing):.4f}, NRSE = {algo.rse[-1]:.4e}")
