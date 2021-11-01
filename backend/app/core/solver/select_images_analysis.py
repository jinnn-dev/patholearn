from typing import List, Tuple


class SelectImagesAnalysis:
    @staticmethod
    def check_select_images(*, task_solution: List[str], user_solution: List[str]) -> Tuple[List[str], List[str]]:
        """
        Checks whether the user selected all images in the task solution or not.
        Returns all correcty and wrongly selected image indices.

        :param task_solution: Task solution
        :param user_solution: User solution
        :return: The solve result
        """

        correct_images = []
        wrong_images = []

        for image_index in user_solution:
            if image_index in task_solution:
                correct_images.append(image_index)
            else:
                wrong_images.append(image_index)

        return correct_images, wrong_images
