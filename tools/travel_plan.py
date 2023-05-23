# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 21:52
# @Author  : 
# @File    : travel_plan.py
# @Software: PyCharm 
# @Comment :
from langchain.tools.base import BaseTool


class TravelPlanTool(BaseTool):
    name = "Travel Plan"
    description = (
        "当你想生成旅行计划时使用这个工具。"
        "输入为用户需求，如：北京，5天"
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        return f"""旅行计划范本：
Day 1: Exploring Beijing's Historic Sites 
Morning: Start the day early with a visit to The Forbidden City, an ancient imperial palace that used to be the residence of emperors during the Ming and Qing dynasties. 

Afternoon: After lunch visit the Tiananmen Square, a historic city square and the site of several important events in Chinese history.

Evening: End the day by taking a stroll through Houhai Lake, a charming lake surrounded by trendy bars and cafes.

Day 2: The Great Wall and Peking Duck 
Morning: Prepare yourself for an awe-inspiring experience at one of the world wonders - The Great Wall of China. Visit the Mutianyu section which is less crowded and offers breathtaking views of the surrounding hills.

Afternoon: Grab a bite to eat and try Beijing's famous Peking Duck for lunch at Quanjude Roast Duck, a well-known restaurant that serves this luxury delicacy.

Evening: Head back to the city and visit The Temple of Heaven for a visual treat of stunning architecture. The park surrounding the temple is a beautiful respite.

Day 3: Exploring Hutongs and Summer Palace 
Morning: Walk through the ancient alleys of Hutongs and witness daily life of Beijing people.

Afternoon: Visit The Summer Palace, an extensive lakeside retreat that encapsulates Chinese landscape garden style.

Evening: Enjoy the lively atmosphere in Sanlitun, one of the city’s most modern and international districts dotted with numerous shopping centres, bars, and restaurants.

Day 4: Exploring Local Cultures and Markets 
Morning: Visit the world-renowned attraction Temple of Confucius, a serene and ancient temple complex dedicated to China’s most illustrious philosopher.

Afternoon: Relish in local cuisine by visiting Wangfujing Snack Street, the best place to try different types of Chinese street food.

Evening: Head to Panjiayuan Market, Beijing’s largest antiques market. It offers endless options of antique relics, traditional folk handicrafts, and artwork, which make excellent souvenirs.

Day 5: Day trip to the Palace Museum and Silk Market 
Morning: Take a day trip to the serene Palace Museum which has a vast collection of Chinese art and artifacts dating back to the Ming and Qing dynasties.

Afternoon: Head to Silk Market, a seven-story shopping mall that has everything from luxury brands to souvenirs.

Evening: End the day by taking in the iconic views of Beijing CBD Skyscrapers from from one of the bars in China World Summit Wing.
------

直接根据用户提供的需求信息：【{query}】，参考上面的旅行计划范本，以‘好的，下面是根据您需求生成的旅行计划’开头，生成详细的中文旅行计划，按照Option #2格式输出。"""

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)
