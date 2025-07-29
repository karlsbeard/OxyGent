import os
import base64
import pytest
from unittest.mock import AsyncMock, patch, MagicMock, mock_open
from mcp_servers.browser_tools import browser_take_screenshot, check_dependencies

class TestBrowserTakeScreenshot:
    @pytest.fixture
    async def mock_page(self):
        page = AsyncMock()
        page.screenshot = AsyncMock()
        return page
    
    @pytest.fixture
    async def mock_ensure_page(self, mock_page):
        with patch('mcp_servers.browser_tools._ensure_page', return_value=mock_page):
            yield mock_page

    @pytest.mark.asyncio
    async def test_save_screenshot_to_file(self, mock_ensure_page, tmp_path):
        # 准备测试数据
        test_path = os.path.join(tmp_path, "test_screenshot.png")
        mock_ensure_page.screenshot.return_value = b"test image data"
        
        # 执行测试
        result = await browser_take_screenshot(path=test_path)
        
        # 验证结果
        assert isinstance(result, dict)
        assert result["path"] == test_path
        assert "size_mb" in result
        mock_ensure_page.screenshot.assert_called_once_with(full_page=False)

    @pytest.mark.asyncio
    async def test_save_to_cache_dir(self, mock_ensure_page):
        # 准备测试数据
        test_bytes = b"test image data"
        mock_ensure_page.screenshot.return_value = test_bytes
        
        # 模拟cache_dir路径
        mock_cache_path = "/fake/path/cache_dir/screenshot_20250729_123456_abcd1234.png"
        
        # 模拟os.getcwd, datetime.now和uuid.uuid4
        with patch('os.getcwd', return_value="/fake/path"), \
             patch('os.makedirs') as mock_makedirs, \
             patch('datetime.now') as mock_now, \
             patch('uuid.uuid4') as mock_uuid, \
             patch('builtins.open', mock_open()) as mock_file:
            
            # 设置模拟返回值
            mock_now.return_value.strftime.return_value = "20250729_123456"
            mock_uuid.return_value = type('obj', (object,), {'__str__': lambda self: "abcd1234efgh5678"})()
            
            # 执行测试
            result = await browser_take_screenshot()
            
            # 验证结果
            assert isinstance(result, dict)
            assert result["path"] == mock_cache_path
            assert "size_mb" in result
            mock_makedirs.assert_called_once_with("/fake/path/cache_dir", exist_ok=True)
            mock_file.assert_called_once_with(mock_cache_path, 'wb')
            mock_file().write.assert_called_once_with(test_bytes)
        
        mock_ensure_page.screenshot.assert_called_once_with(full_page=False)

    @pytest.mark.asyncio
    async def test_full_page_screenshot(self, mock_ensure_page, tmp_path):
        # 准备测试数据
        test_path = os.path.join(tmp_path, "test_full_screenshot.png")
        mock_ensure_page.screenshot.return_value = b"test full page image data"
        
        # 执行测试
        result = await browser_take_screenshot(path=test_path, full_page=True)
        
        # 验证结果
        assert isinstance(result, dict)
        assert result["path"] == test_path
        assert "size_mb" in result
        mock_ensure_page.screenshot.assert_called_once_with(full_page=True)

    @pytest.mark.asyncio
    async def test_missing_dependencies(self):
        # 模拟缺少依赖
        with patch('mcp_servers.browser_tools.check_dependencies', return_value=['playwright']):
            result = await browser_take_screenshot()
            assert "缺少必要的库" in result
            assert "playwright" in result

    @pytest.mark.asyncio
    async def test_screenshot_error(self, mock_ensure_page):
        # 模拟截图错误
        mock_ensure_page.screenshot.side_effect = Exception("截图失败")
        
        # 执行测试
        result = await browser_take_screenshot()
        
        # 验证结果
        assert "截取页面截图时发生错误" in result
        assert "截图失败" in result

    @pytest.mark.asyncio
    async def test_invalid_path(self, mock_ensure_page):
        # 准备测试数据：使用无效路径
        invalid_path = "/invalid/path/screenshot.png"
        mock_ensure_page.screenshot.return_value = b"test image data"  # 返回正常数据
        # 模拟写入文件时出错
        with patch('builtins.open', side_effect=Exception("无法保存到指定路径")):
            # 执行测试
            result = await browser_take_screenshot(path=invalid_path)
            
            # 验证结果
            assert isinstance(result, str)
            assert "截取页面截图时发生错误" in result
            assert "无法保存到指定路径" in result