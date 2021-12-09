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

from tencentcloud.common.abstract_model import AbstractModel


class DeployApplicationRequest(AbstractModel):
    """DeployApplication请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class DeployApplicationResponse(AbstractModel):
    """DeployApplication返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetApplicationStatusRequest(AbstractModel):
    """GetApplicationStatus请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class GetApplicationStatusResponse(AbstractModel):
    """GetApplicationStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetComponentAndVersionsRequest(AbstractModel):
    """GetComponentAndVersions请求参数结构体

    """

    def __init__(self):
        """
        :param ComponentName: Component Name
        :type ComponentName: str
        """
        self.ComponentName = None


    def _deserialize(self, params):
        self.ComponentName = params.get("ComponentName")


class GetComponentAndVersionsResponse(AbstractModel):
    """GetComponentAndVersions返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetComponentVersionRequest(AbstractModel):
    """GetComponentVersion请求参数结构体

    """

    def __init__(self):
        """
        :param ComponentName: Component Name
        :type ComponentName: str
        :param ComponentVersion: Component Version
        :type ComponentVersion: str
        """
        self.ComponentName = None
        self.ComponentVersion = None


    def _deserialize(self, params):
        self.ComponentName = params.get("ComponentName")
        self.ComponentVersion = params.get("ComponentVersion")


class GetComponentVersionResponse(AbstractModel):
    """GetComponentVersion返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetDeploymentStatusRequest(AbstractModel):
    """GetDeploymentStatus请求参数结构体

    """

    def __init__(self):
        """
        :param JobBuildId: Job Build Id
        :type JobBuildId: str
        :param Body: JSON stringified object
        :type Body: str
        """
        self.JobBuildId = None
        self.Body = None


    def _deserialize(self, params):
        self.JobBuildId = params.get("JobBuildId")
        self.Body = params.get("Body")


class GetDeploymentStatusResponse(AbstractModel):
    """GetDeploymentStatus返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetInstanceRequest(AbstractModel):
    """GetInstance请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        :param InstanceName: Instance Name
        :type InstanceName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")
        self.InstanceName = params.get("InstanceName")


class GetInstanceResponse(AbstractModel):
    """GetInstance返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetPackageRequest(AbstractModel):
    """GetPackage请求参数结构体

    """

    def __init__(self):
        """
        :param PackageName: Package Name
        :type PackageName: str
        :param PackageVersion: Package Version
        :type PackageVersion: str
        """
        self.PackageName = None
        self.PackageVersion = None


    def _deserialize(self, params):
        self.PackageName = params.get("PackageName")
        self.PackageVersion = params.get("PackageVersion")


class GetPackageResponse(AbstractModel):
    """GetPackage返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class GetUploadUrlsRequest(AbstractModel):
    """GetUploadUrls请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class GetUploadUrlsResponse(AbstractModel):
    """GetUploadUrls返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class ListComponentsRequest(AbstractModel):
    """ListComponents请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class ListComponentsResponse(AbstractModel):
    """ListComponents返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class ListInstancesRequest(AbstractModel):
    """ListInstances请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")


class ListInstancesResponse(AbstractModel):
    """ListInstances返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class ListPackagesRequest(AbstractModel):
    """ListPackages请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class ListPackagesResponse(AbstractModel):
    """ListPackages返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class ListParametersRequest(AbstractModel):
    """ListParameters请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")


class ListParametersResponse(AbstractModel):
    """ListParameters返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class PostPublishComponentRequest(AbstractModel):
    """PostPublishComponent请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param ComponentName: Component Name
        :type ComponentName: str
        :param ComponentVersion: Component Version
        :type ComponentVersion: str
        """
        self.Body = None
        self.ComponentName = None
        self.ComponentVersion = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.ComponentName = params.get("ComponentName")
        self.ComponentVersion = params.get("ComponentVersion")


class PostPublishComponentResponse(AbstractModel):
    """PostPublishComponent返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class PostPublishPackageRequest(AbstractModel):
    """PostPublishPackage请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class PostPublishPackageResponse(AbstractModel):
    """PostPublishPackage返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class PrePublishComponentRequest(AbstractModel):
    """PrePublishComponent请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param ComponentName: Component Name
        :type ComponentName: str
        :param ComponentVersion: Component Version
        :type ComponentVersion: str
        """
        self.Body = None
        self.ComponentName = None
        self.ComponentVersion = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.ComponentName = params.get("ComponentName")
        self.ComponentVersion = params.get("ComponentVersion")


class PrePublishComponentResponse(AbstractModel):
    """PrePublishComponent返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class PreparePublishPackageRequest(AbstractModel):
    """PreparePublishPackage请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        """
        self.Body = None


    def _deserialize(self, params):
        self.Body = params.get("Body")


class PreparePublishPackageResponse(AbstractModel):
    """PreparePublishPackage返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class RunComponentRequest(AbstractModel):
    """RunComponent请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        :param InstanceName: Instance Name
        :type InstanceName: str
        :param Channel: Channel URL
        :type Channel: str
        :param RoleName: Role Name
        :type RoleName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None
        self.InstanceName = None
        self.Channel = None
        self.RoleName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")
        self.InstanceName = params.get("InstanceName")
        self.Channel = params.get("Channel")
        self.RoleName = params.get("RoleName")


class RunComponentResponse(AbstractModel):
    """RunComponent返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class RunFinishComponentRequest(AbstractModel):
    """RunFinishComponent请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        :param InstanceName: Instance Name
        :type InstanceName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")
        self.InstanceName = params.get("InstanceName")


class RunFinishComponentResponse(AbstractModel):
    """RunFinishComponent返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class SaveInstanceRequest(AbstractModel):
    """SaveInstance请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage  Name
        :type StageName: str
        :param InstanceName: Instance Name
        :type InstanceName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None
        self.InstanceName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")
        self.InstanceName = params.get("InstanceName")


class SaveInstanceResponse(AbstractModel):
    """SaveInstance返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")


class SendCouponRequest(AbstractModel):
    """SendCoupon请求参数结构体

    """

    def __init__(self):
        """
        :param Type: 发送代金券类型(活动tag)
        :type Type: list of str
        """
        self.Type = None


    def _deserialize(self, params):
        self.Type = params.get("Type")


class SendCouponResponse(AbstractModel):
    """SendCoupon返回参数结构体

    """

    def __init__(self):
        """
        :param Msg: 错误描述
注意：此字段可能返回 null，表示取不到有效值。
        :type Msg: str
        :param ReturnCode: 错误代码,为0成功
        :type ReturnCode: int
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Msg = None
        self.ReturnCode = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Msg = params.get("Msg")
        self.ReturnCode = params.get("ReturnCode")
        self.RequestId = params.get("RequestId")


class SetParameterRequest(AbstractModel):
    """SetParameter请求参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object
        :type Body: str
        :param AppName: App Name
        :type AppName: str
        :param StageName: Stage Name
        :type StageName: str
        """
        self.Body = None
        self.AppName = None
        self.StageName = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.AppName = params.get("AppName")
        self.StageName = params.get("StageName")


class SetParameterResponse(AbstractModel):
    """SetParameter返回参数结构体

    """

    def __init__(self):
        """
        :param Body: JSON stringified object containing response payload.
        :type Body: str
        :param RequestId: 唯一请求 ID，每次请求都会返回。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self.Body = None
        self.RequestId = None


    def _deserialize(self, params):
        self.Body = params.get("Body")
        self.RequestId = params.get("RequestId")