from core.parser import parse
from core.package import Package


def test_parse_simple():
    input_data = r"""
    /code/modules-mobilebanking/Modules.MobileBanking.API/Modules.MobileBanking.API.csproj : error NU1102: Unable to find package ApplicationLogic.Contract with version (>= 1.1.0)
    /code/modules-mobilebanking/Modules.MobileBanking.API/Modules.MobileBanking.API.csproj : error NU1102:   - Found 2 version(s) in GitLab [ Nearest version: 1.1.0 ]
    /code/modules-mobilebanking/Modules.MobileBanking.API/Modules.MobileBanking.API.csproj : error NU1102:   - Found 0 version(s) in nuget.org
    """

    output = parse(input_data)
    print(output)
    assert output == [Package(name="applicationlogic.contract", version="1.1.0")]


def test_parse_multiple():
    input_data = r"""
    Determining projects to restore...

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.CodeAnalysis.FxCopAnalyzers. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.EntityFrameworkCore. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.EntityFrameworkCore.Design. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.EntityFrameworkCore.SqlServer. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.EntityFrameworkCore.Tools. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.Extensions.DependencyInjection.Abstractions. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.Extensions.Logging.Abstractions. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj : error NU1101: Unable to find package Microsoft.Extensions.Options. No packages exist with this id in source(s): Microsoft Visual Studio Offline Packages [D:\a\1\s\Megatron.sln]

    Failed to restore D:\a\1\s\src\Megatron.Saleslogix\Megatron.Saleslogix.csproj (in 467 ms).

    Restored D:\a\1\s\src\Orchard.Abstractions\Orchard.Abstractions.csproj (in 28.59 sec).

    Restored D:\a\1\s\src\Megatron.Core\Megatron.Core.csproj (in 1.17 min).

    Restored D:\a\1\s\test\Orchard.Abstractions.Tests\Orchard.Abstractions.Tests.csproj (in 18.42 sec).

    Restored D:\a\1\s\test\Megatron.Core.Tests\Megatron.Core.Tests.csproj (in 1.03 min).

    Restored D:\a\1\s\test\Megatron.Saleslogix.Tests\Megatron.Saleslogix.Tests.csproj (in 1.5 min).

    Restored D:\a\1\s\src\Megatron.Web\Megatron.Web.csproj (in 1.51 min).

    Restored D:\a\1\s\test\Megatron.Web.Tests\Megatron.Web.Tests.csproj (in 310 ms).

    ##[error]Cmd.exe exited with code '1'.
    """

    output = parse(input_data)
    print(output)
    assert output == [
        Package(name="microsoft.codeanalysis.fxcopanalyzers", version=None),
        Package(name="microsoft.entityframeworkcore", version=None),
        Package(name="microsoft.entityframeworkcore.design", version=None),
        Package(name="microsoft.entityframeworkcore.sqlserver", version=None),
        Package(name="microsoft.entityframeworkcore.tools", version=None),
        Package(
            name="microsoft.extensions.dependencyinjection.abstractions", version=None
        ),
        Package(name="microsoft.extensions.logging.abstractions", version=None),
        Package(name="microsoft.extensions.options", version=None),
    ]


def test_parse_downgrade():
    input_data = r"""
    error NU1605: Detected package downgrade: Ucsb.Sa.Enterprise.AspNetCore.Mvc.Hosting from 5.0.66833 to 5.0.65698. Reference the package directly from the project to select a different version.  [D:\TFS\2\_work\10\s\Ucsb.Sa.GradDiv.CampusContacts.Web.sln] 
    """

    output = parse(input_data)
    print(output)
    assert output == [
        Package(name="ucsb.sa.enterprise.aspnetcore.mvc.hosting", version="5.0.65698"),
        Package(name="ucsb.sa.enterprise.aspnetcore.mvc.hosting", version="5.0.66833"),
    ]
