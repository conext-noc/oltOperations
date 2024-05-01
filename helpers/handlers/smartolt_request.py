import os
from helpers.constants.definitions import Client, List, Union, Dict, ClientRequest
from dotenv import load_dotenv

load_dotenv()


class SmartOLT:
    """This class handles all SmartOLT Connection handlers like, get_onus/update_onus"""

    def __init__(self, method: str, data: List[Client]) -> None:
        """Initializer class

        Args:
            method (str): _description_
            data (Dict): _description_
        """
        self.method = method
        # self.endpoint = endpoint
        self.data = data
        self.token = os.getenv("SMART_OLT_API_KEY")
        self.header = "X-Token"

    def get_client(
        self,
        is_bulk: bool,
        data: Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]],
    ) -> Dict[str, Union[List[Client], str, bool]]:
        """_summary_

        Args:
            is_bulk (bool): _description_
            data (Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]]): _description_

        Returns:
            Dict[str, Union[List[Client], str, bool]]: _description_
        """

    def update_client(
        self,
        is_bulk: bool,
        data: Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]],
    ) -> Dict[str, Union[List[Client], str, bool]]:
        """_summary_

        Args:
            is_bulk (bool): _description_
            data (Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]]): _description_

        Returns:
            Dict[str, Union[List[Client], str, bool]]: _description_
        """

    def delete_client(
        self,
        is_bulk: bool,
        data: Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]],
    ) -> Dict[str, Union[List[Client], str, bool]]:
        """_summary_

        Args:
            is_bulk (bool): _description_
            data (Union[List[Union[ClientRequest, Dict[str, str]], ClientRequest]]): _description_

        Returns:
            Dict[str, Union[List[Client], str, bool]]: _description_
        """
