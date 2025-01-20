from .ai_agent import AIAgent
from .backend_agent import BackendAgent
from .frontend_agent import FrontendAgent
from .design_agent import DesignAgent
from .product_agent import ProductAgent

def create_agent(agent_type):
    agents = {
        'ai': AIAgent,
        'backend': BackendAgent,
        'frontend': FrontendAgent,
        'design': DesignAgent,
        'product': ProductAgent
    }
    return agents[agent_type]()
