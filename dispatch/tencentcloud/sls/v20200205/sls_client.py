# -*- coding: utf8 -*-
# Copyright (c) 2017-2018 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.sls.v20200205 import models


class SlsClient(AbstractClient):
    _apiVersion = '2020-02-05'
    _endpoint = 'sls.tencentcloudapi.com'


    def DeployApplication(self, request):
        """部署应用

        :param request: Request instance for DeployApplication.
        :type request: :class:`tencentcloud.sls.v20200205.models.DeployApplicationRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.DeployApplicationResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeployApplication", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeployApplicationResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetApplicationStatus(self, request):
        """获取应用状态

        :param request: Request instance for GetApplicationStatus.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetApplicationStatusRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetApplicationStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetApplicationStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetApplicationStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetComponentAndVersions(self, request):
        """该接口获取指定Component的所有版本信息

        :param request: Request instance for GetComponentAndVersions.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetComponentAndVersionsRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetComponentAndVersionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetComponentAndVersions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetComponentAndVersionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetComponentVersion(self, request):
        """获取指定name和版本的Component信息

        :param request: Request instance for GetComponentVersion.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetComponentVersionRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetComponentVersionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetComponentVersion", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetComponentVersionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetDeploymentStatus(self, request):
        """获取应用部署状态

        :param request: Request instance for GetDeploymentStatus.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetDeploymentStatusRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetDeploymentStatusResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetDeploymentStatus", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetDeploymentStatusResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetInstance(self, request):
        """用户获取一个已部署Component的Instance

        :param request: Request instance for GetInstance.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetInstanceRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetPackage(self, request):
        """获取Package的详细信息

        :param request: Request instance for GetPackage.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetPackageRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetPackageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetPackage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetPackageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def GetUploadUrls(self, request):
        """用户获取Component Instance的预签名URL链接

        :param request: Request instance for GetUploadUrls.
        :type request: :class:`tencentcloud.sls.v20200205.models.GetUploadUrlsRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.GetUploadUrlsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("GetUploadUrls", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.GetUploadUrlsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListComponents(self, request):
        """用户获取Component的列表信息

        :param request: Request instance for ListComponents.
        :type request: :class:`tencentcloud.sls.v20200205.models.ListComponentsRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.ListComponentsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListComponents", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListComponentsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListInstances(self, request):
        """用户获取一个已部署Component的Instance列表

        :param request: Request instance for ListInstances.
        :type request: :class:`tencentcloud.sls.v20200205.models.ListInstancesRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.ListInstancesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListInstances", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListInstancesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListPackages(self, request):
        """获取Package的列表信息

        :param request: Request instance for ListPackages.
        :type request: :class:`tencentcloud.sls.v20200205.models.ListPackagesRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.ListPackagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListPackages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListPackagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ListParameters(self, request):
        """获取parameter列表

        :param request: Request instance for ListParameters.
        :type request: :class:`tencentcloud.sls.v20200205.models.ListParametersRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.ListParametersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ListParameters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ListParametersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PostPublishComponent(self, request):
        """发布一个指定name和version的Component

        :param request: Request instance for PostPublishComponent.
        :type request: :class:`tencentcloud.sls.v20200205.models.PostPublishComponentRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.PostPublishComponentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PostPublishComponent", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PostPublishComponentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PostPublishPackage(self, request):
        """发布一个指定name和version的Package

        :param request: Request instance for PostPublishPackage.
        :type request: :class:`tencentcloud.sls.v20200205.models.PostPublishPackageRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.PostPublishPackageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PostPublishPackage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PostPublishPackageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PrePublishComponent(self, request):
        """预发布一个指定name和version的Component

        :param request: Request instance for PrePublishComponent.
        :type request: :class:`tencentcloud.sls.v20200205.models.PrePublishComponentRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.PrePublishComponentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PrePublishComponent", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PrePublishComponentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PreparePublishPackage(self, request):
        """预发布一个指定name和version的Package

        :param request: Request instance for PreparePublishPackage.
        :type request: :class:`tencentcloud.sls.v20200205.models.PreparePublishPackageRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.PreparePublishPackageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PreparePublishPackage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PreparePublishPackageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RunComponent(self, request):
        """运行一个Component

        :param request: Request instance for RunComponent.
        :type request: :class:`tencentcloud.sls.v20200205.models.RunComponentRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.RunComponentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RunComponent", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RunComponentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RunFinishComponent(self, request):
        """运行完成Component，更新Component Instance信息

        :param request: Request instance for RunFinishComponent.
        :type request: :class:`tencentcloud.sls.v20200205.models.RunFinishComponentRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.RunFinishComponentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RunFinishComponent", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RunFinishComponentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SaveInstance(self, request):
        """用户保存一个已部署Component的Instance

        :param request: Request instance for SaveInstance.
        :type request: :class:`tencentcloud.sls.v20200205.models.SaveInstanceRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.SaveInstanceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SaveInstance", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SaveInstanceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendCoupon(self, request):
        """发送代金券

        :param request: Request instance for SendCoupon.
        :type request: :class:`tencentcloud.sls.v20200205.models.SendCouponRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.SendCouponResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendCoupon", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendCouponResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SetParameter(self, request):
        """设置Parameter

        :param request: Request instance for SetParameter.
        :type request: :class:`tencentcloud.sls.v20200205.models.SetParameterRequest`
        :rtype: :class:`tencentcloud.sls.v20200205.models.SetParameterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SetParameter", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SetParameterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)