from fastai.tabular import *

from .databunch import DashTabularDatabunch
from .loss import DashTabularLoss
from .metric import DashTabularMetric
from .model import DashTabularModel
from .optimizer import DashTabularOptimizer


class DashTabularLearner:

	@staticmethod
	def create_tabular_learner(response):

		path = Path('./')
		databunch = DashTabularDatabunch.create_tabular_databunch(response)
		metrics = DashTabularMetric.create_tabular_metric(response["core"])

		if response["tabular"]["model"]["type"] == "default":
			model = DashTabularModel.create_tabular_model(databunch, response["tabular"]['model'])

		loss = DashTabularLoss.create_tabular_loss(response["core"]['loss'])
		opt = DashTabularOptimizer.create_tabular_optimizer(response["core"]['optimizer'])

		# learn = Learner(
		# 	databunch,
		# 	model,
		# 	metrics=metrics,
		# 	opt_func=opt,
		# 	loss_func=loss
		# )

		# return learn

		# Test it out
		if response["tabular"]["model"]["type"] == "custom":
			layers = [eval(l) for l in response["tabular"]['model']['custom']['layers']]
			model = DashTabularModel.create_custom_tabular_model(databunch, layers,
																 **response["tabular"]["model"]["custom"]["extra_args"])
			learn = Learner(databunch, model, metrics=metrics, loss_func=loss, opt_func=opt)
			return learn

		learn = tabular_learner(
			databunch,
			layers=response['tabular']['model']['default']['layers'],
			metrics=metrics,
			opt_func=opt,
			loss_func=loss  # Passing loss gives errors
		)

		return learn
