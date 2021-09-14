class FeedbackConfig:
    BORDER_DECENT = 0.3
    LOWER_AREA_BORDER = 0.9
    UPPER_AREA_BORDER = 1.9
    PERCENTAGE_LENGTH_DIFFERENCE = 0.6
    PERCENTAGE_OUTSIDE = 0.1

    @staticmethod
    def get_weighted_border(*, border: float, knowledge_level: int, decent_value: float = BORDER_DECENT) -> float:
        """
        Returns the new border weighted by the given knowledge level and decent value.
        Multiplies knowledge level with decent value to get the new border

        :param border: Unweighted border
        :param knowledge_level: Knowledge level to weight the border
        :param decent_value: The weight
        :return: The weighted border
        """
        return border - decent_value * knowledge_level
