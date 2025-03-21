from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from lxml import etree


class BaseXMLParser(ABC):
    """
    Abstract base class for parsing XML files using lxml.
    Intended to be subclassed by concrete parsers for specific XML schemas.
    """

    parser = etree.XMLParser(recover=True)

    def __init__(self, file: Path):
        """
        Initializes the parser with a given XML file.

        Args:
            file (Path): Path to the XML file to be parsed.
        """
        self.file = file
        self.tree = etree.parse(file, parser=self.parser)
        self.root = self.tree.getroot()
        self.namespaces = self._register_namespaces()

    @abstractmethod
    def parse(self) -> dict:
        """
        Parses the XML and returns relevant data as a dictionary.
        Must be implemented by subclasses.

        Returns:
            dict: Parsed data extracted from the XML.
        """
        pass

    @abstractmethod
    def _register_namespaces(self) -> dict:
        """
        Registers XML namespaces required for XPath queries.
        Must be implemented by subclasses.

        Returns:
            dict: A mapping of prefix to namespace URI.
        """
        pass

    def get_descendants(self, xpath_expr: str) -> List[etree.Element]:
        """
        Returns all elements that match the given XPath expression.

        Args:
            xpath_expr (str): The XPath expression to evaluate.

        Returns:
            List[etree.Element]: A list of matching elements.
        """
        return self.root.xpath(xpath_expr, namespaces=self.namespaces)

    def get_first_descendant(self, xpath_expr: str) -> Optional[etree.Element]:
        """
        Returns the first element that matches the given XPath expression, if any.

        Args:
            xpath_expr (str): The XPath expression to evaluate.

        Returns:
            Optional[etree.Element]: The first matching element, or None if not found.
        """
        results = self.get_descendants(xpath_expr)
        return results[0] if results else None
