from src.core.browser import BrowserManager
from src.services.loop_controller import LoopController

if __name__ == "__main__":
    with BrowserManager() as page:
        BrowserManager.login(page)
        controller = LoopController(page)
        controller.run() 