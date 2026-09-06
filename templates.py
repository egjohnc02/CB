GREETING_TEMPLATE = """Hello,

I have received your request and will begin working on this ticket. Please monitor this ticket closely in case any additional information is needed.

Thank you,
Tu Nguyen"""


MANDARIN_GREETING_TEMPLATE = """我们很高兴为您提供中英双语服务。接下来您可以任意选择中文或英文来更新此工单。

尊敬的供应商团队， 

您好！

我们已收到您的请求，并将开始处理此工单。 

请您密切关注此工单，以便在需要时提供补充信息。 

祝好，

Tu Nguyen


We’re happy to support you in both Mandarin and English. Please feel free to continue the conversation in your preferred language.

Hello,

I have received your request and will begin working on this ticket. Please monitor this ticket closely in case any additional information is needed.

Thank you,
Tu Nguyen"""


NORMAL_DONE_TEMPLATE = """Hello,

We have finished this ticket today. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


MANDARIN_NORMAL_DONE_TEMPLATE = """尊敬的供应商团队，

您好！

此工单已于今日完成。详细信息请参阅附件。

请等待 24-48 小时，以便更改在网站上生效。如果在 48 小时后更改仍未显示，请添加评论以重新开启工单，我们将继续协助您解决此问题。

如您有新的更新需求，请提交一张新的工单。

祝好，

Tu Nguyen


Hello,

We have finished this ticket today. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


EXCLUDED_DONE_TEMPLATE = """Hello,

We have finished this ticket today, but {number} SKUs have been excluded from the request due to {reason}. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


MANDARIN_EXCLUDED_DONE_TEMPLATE = """尊敬的供应商团队，

您好！

此工单已于今日完成，但由于 {reason}，已有 {number} 个 SKU 从请求中排除。详细信息请参阅附件。

请等待 24-48 小时，以便更改在网站上生效。如果在 48 小时后更改仍未显示，请添加评论以重新开启工单，我们将继续协助您解决此问题。

如您有新的更新需求，请提交一张新的工单。

祝好，

Tu Nguyen


Hello,

We have finished this ticket today, but {number} SKUs have been excluded from the request due to {reason}. Details can be found in this attachment.
Please allow 24-48 hours for changes to reflect on-site. If changes are not displayed after this time, please add a comment to reopen the ticket and we will work on resolving the issue. If you have a new request to have updates made, we would ask that a new ticket be entered!

Thank you,
Tu Nguyen"""


# ============================================================
# CANCEL TEMPLATES
# ============================================================

CANCEL_REROUTE_TEMPLATE = """[Public Comment]
Hello,

We've completed request [{request_id}]. I am rerouting this ticket to the {team_name} to {update_details}. They will provide you with an update shortly!

Thank you,
Tu Nguyen

----------------------------------------
[Internal Note]
Team: {target_team}
Initial Update: {initial_update}
Summary: {summary}
Action Requested: {action_requested}
Next Steps: {next_steps}"""


CANCEL_ONSITE_TEMPLATE = """Hello,

Thank you for reaching out regarding the storefront issue. We have flagged your concern to our tech team for further investigation. We will be closing this ticket while the tech team assists.

Please let us know if you have any questions.

Best Regards,
Tu Nguyen"""


CANCEL_DUPLICATE_TEMPLATE = """Hi Supplier Team,

Thank you for your request. Upon further checking, we have confirmed that this ticket request is a duplicate of the ticket request {original_ticket}. Please expect an update on {original_ticket} itself soon.

We will be closing this duplicate ticket. If you have any questions or feel like the request is different from the duplicate ticket, please don't hesitate to reopen this ticket. Thank you for your understanding.

Thank you,
Tu Nguyen"""


CANCEL_ALREADY_IN_TARGET_TEMPLATE = """Hello,

Upon our checking, SKU {sku} is currently under the {target_type} ({target_name}).

Since no further action from our end is needed, we will be closing this ticket.

Thank you,
Tu Nguyen"""


CANCEL_SF_DISPLAY_BUG_TEMPLATE = """Hello, thank you for your ticket

We are currently experiencing issues with our replatformed SF display and have submitted a ticket flagging your concern. We will be closing this ticket while the tech team assists.

Please let us know if you have any questions,
Tu Nguyen"""


CANCEL_WAITING_AUTHOR_3DAYS_TEMPLATE = """Hello,

This ticket has surpassed its time on pause, so we will be closing this ticket. We ask that once you have the clarification we need to proceed with completing this ticket, you leave a comment on this ticket to re-open it.

Thanks,
Tu Nguyen"""


MANDARIN_CANCEL_WAITING_AUTHOR_3DAYS_TEMPLATE = """尊敬的供应商团队，
您好！

此工单已等待超 3 天时间，因此我们将关闭该工单。

待您补齐所需信息，我方可以继续处理后，请在该工单下留言以重新开启。

祝好，
Tu Nguyen"""


CANCEL_MASTER_NOT_CORE_CLASS_TEMPLATE = """Hello,

The reason this SKU [or these SKUs] could not be moved into Exclusive Brands is because their Master Class is not a Core Class (meaning it is a class Wayfair does not have in our Exclsuive Brands). Some factors as to why some classes are ineligible for White Labeling are that the classes are primarily style agnostic, and are differentiated based on function. Additionally, classes that are more likely to be recognized by brand name (such as appliances) are excluded.

Thank you,
Tu Nguyen"""


MANDARIN_CANCEL_MASTER_NOT_CORE_CLASS_TEMPLATE = """尊敬的供应商团队，
您好！

该 SKU ___ 无法被移入 Wayfair 独家品牌的原因是，其主类别（Master Class）并非核心类别（Core Class）（即该类别不在 Wayfair 独家品牌的收录范围内）。部分类别无法成为白牌产品主要原因：这类型类别大多无固定款式区分，仅依靠产品功能划分；此外，家电等依靠品牌辨识度区分的类别，同样不在 Wayfair 独家品牌准入范围内。

祝好，
Tu Nguyen"""


CANCEL_BAD_STATUS_TEMPLATE = """Hello,

The reason this SKU [or these SKUs] could not be moved into Exclusive Brands is because they are not live on-site. Our tools are only able to process SKUs that are live on Wayfair's site. There are a variety of "bad statuses" that make a SKU inaccesssible on site, and thus, unable to be moved into Exclusive Brands. Examples of bad statuses include "Supplier Discontinued" and "Missing Imagery." [if responding to exclusion] Please reach out to Findability to correct this, then submit a subsequent White Label ticket.

Thank you, 
Tu Nguyen"""


CANCEL_MULTI_SOURCE_SKU_TEMPLATE = """Hello,

We have completed this ticket today, but cannot proceed with the request of {number} SKUs because of the sku set up. Suppliers should reach out to their Supplier Relationship Manager or Category Manager with any questions about the excluded SKUs, and Wayfair employees should reach out to #merch-cat-mgmt-help.

Thank you, 
Tu Nguyen"""


# ============================================================
# ON HOLD TEMPLATES (STANDARD)
# ============================================================

ON_HOLD_GENERAL_TEMPLATE = """Hello,

Thank you for reaching out. We need additional information to complete your request:

Could you please provide the correct part numbers or SKUs you would like us to proceed with, so we can assist you in resolving the issue?

If we have not received a response in 3 day's time we will close this ticket due to lack of response.

Thank you,
Tu Nguyen"""


ON_HOLD_UNLOCATED_SKU_TEMPLATE = """Hello,

Thank you for reaching out. We need additional information to complete your request:

We are unable to locate the part numbers or SKUs: {skus} under supplier "{supplier}" in our database.

Could you please provide the correct SKUs you would like us to proceed with, so we can assist you in resolving the issue?

If we have not received a response in 3 day's time we will close this ticket due to lack of response.

Thank you,
Tu Nguyen"""


ON_HOLD_IH_SRB_FSB_TEMPLATE = """Hello,

Thank you for your patience. We have started working on your request. Since this request involves a Wayfair Specialty Retail or Flagship brand, we are now waiting for approval from our merchant team to proceed.

Thank you,
Tu Nguyen"""


ON_HOLD_IH_APPROVAL_TEMPLATE = """Hello,

Thank you for your patience. We have started working on your request and are now waiting for our In-House team's review to complete this ticket.

Thank you,
Tu Nguyen"""


ON_HOLD_ENGINEERING_BUG_TEMPLATE = """Hello,

Thank you for your patience. We have started working on the request and We've encountered a {issue_summary} issue that needs the support of engineering to resolve. We will be updating you as soon as information is available. In the meanwhile, this ticket's status will be updated to "Paused."

Thank you,
Tu Nguyen"""


MANDARIN_ON_HOLD_ENGINEERING_BUG_TEMPLATE = """您好！

感谢您的耐心等待。我们已开始处理此工单，但遇到了{issue_summary}问题，需要技术团队协助解决。在收到技术团队的回复后，我们将及时告知您。在此期间，此工单将设为“暂停处理”状态。

谢谢！
Tu Nguyen"""


MANDARIN_ON_HOLD_STUCK_BATCH_TEMPLATE = """您好！

感谢您的耐心等待。我们已开始处理此工单，但遇到了批量任务处理卡顿 (Stuck Batch) 问题，需要技术团队协助解决。在收到技术团队的回复后，我们将及时告知您。在此期间，此工单将设为“暂停处理”状态。

谢谢！
Tu Nguyen"""


ON_HOLD_TOOL_ERROR_TEMPLATE = """Hello,

Thank you for your patience. We are still waiting for engineering to fix tool-related issues. We will be updating you as soon as information is available.

Thank you,
Tu Nguyen"""


MANDARIN_ON_HOLD_TOOL_ERROR_TEMPLATE = """您好！

感谢您的耐心等待。我们已开始处理此工单，但遇到了内部工具故障，需要技术团队协助解决。获取相关信息后，我们将及时告知您。在此期间，此工单将设为暂停状态。

谢谢！
Tu Nguyen"""


ON_HOLD_SPECIFIC_COLLECTION_TEMPLATE = """Hello,

When suppliers agree to participate in our Exclusive Brands program, they do not get to choose the brand or collection name for their SKUs.
If you would still like to update the collection name, Wayfair can assign one for you from a pre-approved list of names.

Please let us know how you would like to proceed.

This ticket will remain open for 3 business days, and if we have not received a response by that time, the ticket will be closed.

Thank you,
Tu Nguyen"""


MANDARIN_ON_HOLD_SPECIFIC_COLLECTION_TEMPLATE = """您好！

当供应商同意加入 Wayfair 独家品牌项目后，供应商就不能自行为 SKU 选择品牌或系列名称。

如您仍需更新系列名称，Wayfair 可从预先批准的名称列表中为您分配名称。

请告知您希望我们如何处理。

我们将保留此工单开启状态 3 个工作日。如届时仍未收到您的回复，将关闭此工单。

谢谢！
Tu Nguyen"""


ON_HOLD_BRAND_CHANGE_TEMPLATE = """Hello,

When suppliers agree to participate in our Exclusive Brands program, they do not get to choose the brand or collection name for their SKUs. If you would still like to move SKUs to a new Exclusive Brand, the Wayfair EB team will decide on the brand for these SKUs based on Wayfair's standards (style and price point), and a new collection name from a pre-approved list of names.

Please let us know how you would like to proceed.

This ticket will remain open for 3 business days, and if we have not received a response by that time, the ticket will be closed.

Thank you,
Tu Nguyen"""


ON_HOLD_TARGET_COLLECTION_INFO_TEMPLATE = """Hello,

We see that you are interested in updating an existing collection, but we need additional information to complete your request. Can you please help us identify the target collection by sharing one or more of the SKUs in the collection you wish to update/move SKUs into?

Thank you,
Tu Nguyen"""


MANDARIN_ON_HOLD_TARGET_COLLECTION_INFO_TEMPLATE = """您好！

我们了解您希望更新现有系列，但我们目前仍需您提供更多额外的信息，才能帮助您完成更新。请您提供目标系列中一个或多个 SKU，以协助我们确认您希望更新或移入 SKU 的目标系列是哪一个。

谢谢！
Tu Nguyen"""


# ============================================================
# ON HOLD TEMPLATES (VAULT / PRIORITY SKU LIST)
# ============================================================

ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could potentially impact:

- Sort rank & PLAs

- SKU Brand

- Product Description

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


MANDARIN_ON_HOLD_VAULT_FULL_WHITE_LABEL_TEMPLATE = """您好！

感谢您就此白牌请求与我们联系！

经确认，{sku_list} 已被列入优先 SKU 列表。由于此产品展示变更可能对以下方面造成影响，因此需要经过更高级别的内部审批：

排序排名和 PLA
SKU 品牌
产品描述

在继续执行您的请求之前，我们会先进行内部审核，以确认是否可以继续推进。请注意，处理时间可能会略有延长。获得批准后，我们将第一时间通过本工单通知您。如您不希望继续推进此请求，请随时告知我们。

感谢您的耐心等待与理解。
Tu Nguyen"""


ON_HOLD_VAULT_PARTIAL_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU brand 

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


MANDARIN_ON_HOLD_VAULT_PARTIAL_WHITE_LABEL_TEMPLATE = """您好！

感谢您就此白牌请求与我们联系！

经确认，{sku_list} 已被列入优先 SKU 列表。由于此产品展示变更可能对以下方面造成影响，因此需要经过更高级别的内部审批：

SKU 品牌

在继续执行您的请求之前，我们会先进行内部审核，以确认是否可以继续推进。请注意，处理时间可能会略有延长。获得批准后，我们将第一时间通过本工单通知您。如您不希望继续推进此请求，请随时告知我们。

感谢您的耐心等待与理解。
Tu Nguyen"""


ON_HOLD_VAULT_COLLECTION_UPDATE_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU collection

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding.
Tu Nguyen"""


MANDARIN_ON_HOLD_VAULT_COLLECTION_UPDATE_TEMPLATE = """您好！

感谢您就此白牌请求与我们联系！

经确认，{sku_list} 已被列入优先 SKU 列表。由于此产品展示变更可能对以下方面造成影响，因此需要经过更高级别的内部审批：

SKU 系列

在继续执行您的请求之前，我们会先进行内部审核，以确认是否可以继续推进。请注意，处理时间可能会略有延长。获得批准后，我们将第一时间通过本工单通知您。如您不希望继续推进此请求，请随时告知我们。

感谢您的耐心等待与理解。
Tu Nguyen"""


ON_HOLD_VAULT_UN_WHITE_LABEL_TEMPLATE = """Hi {name}, 
Thank you for reaching out with this un-white label request.  

We wanted to let you know that {sku_list} {is_are} included in one of our priority SKU lists which now requires elevated internal approval for this merchandising change as it could impact:

- SKU brand

Before moving forward with execution on your request, this request will be internally reviewed to confirm if we can proceed. Please note, this will slightly extend the turnaround time. You will be notified on this ticket if the request is approved. If you no longer want to move forward with this request, please let us know.

Thank you for your patience and understanding. 
Tu Nguyen"""


MANDARIN_ON_HOLD_VAULT_UN_WHITE_LABEL_TEMPLATE = """您好！

感谢您就此取消白牌请求与我们联系！

经确认，{sku_list} 已被列入优先 SKU 列表。由于此产品展示变更可能对以下方面造成影响，因此需要经过更高级别的内部审批：

SKU 品牌

在继续执行您的请求之前，我们会先进行内部审核，以确认是否可以继续推进。请注意，处理时间可能会略有延长。获得批准后，我们将第一时间通过本工单通知您。如您不希望继续推进此请求，请随时告知我们。

感谢您的耐心等待与理解。
Tu Nguyen"""