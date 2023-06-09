from typing import List, NamedTuple

import numpy as np
from IPython import display
from ipycanvas import canvas

from flatland.envs.rail_env import RailEnvActions
from flatland.utils.rendertools import RenderTool


class Behaviour():
    def __init__(self, env):
        self.env = env
        self.nAg = len(env.agents)

    def getActions(self):
        return {}


class AlwaysForward(Behaviour):
    def getActions(self):
        return {i: RailEnvActions.MOVE_FORWARD for i in range(self.nAg)}


class DelayedStartForward(AlwaysForward):
    def __init__(self, env, nStartDelay=2):
        self.nStartDelay = nStartDelay
        super().__init__(env)

    def getActions(self):
        iStep = self.env._elapsed_steps + 1
        nAgentsMoving = min(self.nAg, iStep // self.nStartDelay)
        return {i: RailEnvActions.MOVE_FORWARD for i in range(nAgentsMoving)}


AgentPause = NamedTuple("AgentPause",
                        [
                            ("iAg", int),
                            ("iPauseAt", int),
                            ("iPauseFor", int)
                        ])


class ForwardWithPause(Behaviour):
    def __init__(self, env, lPauses: List[AgentPause]):
        self.env = env
        self.nAg = len(env.agents)
        self.lPauses = lPauses
        self.dAgPaused = {}

    def getActions(self):
        iStep = self.env._elapsed_steps + 1  # add one because this is called before step()

        # new pauses starting this step
        lNewPauses = [tPause for tPause in self.lPauses if tPause.iPauseAt == iStep]

        # copy across the agent index and pause length
        for pause in lNewPauses:
            self.dAgPaused[pause.iAg] = pause.iPauseFor

        # default action is move forward
        dAction = {i: RailEnvActions.MOVE_FORWARD for i in range(self.nAg)}

        # overwrite paused agents with stop
        for iAg in self.dAgPaused:
            dAction[iAg] = RailEnvActions.STOP_MOVING

        # decrement the counters for each pause, and remove any expired pauses.
        lFinished = []
        for iAg in self.dAgPaused:
            self.dAgPaused[iAg] -= 1
            if self.dAgPaused[iAg] <= 0:
                lFinished.append(iAg)

        for iAg in lFinished:
            self.dAgPaused.pop(iAg, None)

        return dAction


class Deterministic(Behaviour):
    def __init__(self, env, dAg_lActions):
        super().__init__(env)
        self.dAg_lActions = dAg_lActions

    def getActions(self):
        iStep = self.env._elapsed_steps

        dAg_Action = {}
        for iAg, lActions in self.dAg_lActions.items():
            if iStep < len(lActions):
                iAct = lActions[iStep]
            else:
                iAct = RailEnvActions.DO_NOTHING
            dAg_Action[iAg] = iAct
        # print(iStep, dAg_Action[0])
        return dAg_Action


class EnvCanvas():

    def __init__(self, env, behaviour: Behaviour = None):
        self.env = env
        self.iStep = 0
        if behaviour is None:
            behaviour = AlwaysForward(env)
        self.behaviour = behaviour
        self.oRT = RenderTool(env, show_debug=True)

        self.oCan = canvas.Canvas(size=(600, 300))
        self.render()

    def render(self):
        self.oRT.render_env(show_rowcols=True, show_inactive_agents=False, show_observations=False)
        gIm = self.oRT.get_image()
        red_channel = gIm[:, :, 0]
        blue_channel = gIm[:, :, 1]
        green_channel = gIm[:, :, 2]
        image_data = np.stack((red_channel, blue_channel, green_channel), axis=2)
        self.oCan.put_image_data(image_data)

    def step(self):
        dAction = self.behaviour.getActions()
        self.env.step(dAction)

    def show(self):
        self.render()
        display.display(self.oCan)
